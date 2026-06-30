import os

base_dir = "/Users/aakashmehta/Desktop/ahoum_spiitual_tech/Spiritual_Tech_Ahoum/frontend/src"
app_dir = os.path.join(base_dir, "app")
components_dir = os.path.join(base_dir, "components")
lib_dir = os.path.join(base_dir, "lib")

os.makedirs(components_dir, exist_ok=True)
os.makedirs(lib_dir, exist_ok=True)
os.makedirs(os.path.join(app_dir, "auth", "login"), exist_ok=True)
os.makedirs(os.path.join(app_dir, "auth", "callback"), exist_ok=True)
os.makedirs(os.path.join(app_dir, "sessions", "[id]"), exist_ok=True)
os.makedirs(os.path.join(app_dir, "dashboard"), exist_ok=True)
os.makedirs(os.path.join(app_dir, "creator"), exist_ok=True)

# 1. lib/api.ts
api_ts = """import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const res = await axios.post(`${API_URL}/api/token/refresh/`, { refresh: refreshToken });
        localStorage.setItem('access_token', res.data.access);
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/auth/login';
      }
    }
    return Promise.reject(error);
  }
);
"""

# 2. lib/auth.tsx
auth_tsx = """'use client';
import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from './api';
import { useRouter } from 'next/navigation';

interface User {
  id: number;
  email: string;
  name?: string;
  role?: string;
  bio?: string;
  avatar_url?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (access: string, refresh: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      api.get('/api/users/me/')
        .then(res => setUser(res.data))
        .catch(() => {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = (access: string, refresh: string) => {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    api.get('/api/users/me/').then(res => {
      setUser(res.data);
      router.push('/dashboard');
    });
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    router.push('/auth/login');
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, isAuthenticated: !!user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
"""

# 3. components/Navbar.tsx
navbar_tsx = """'use client';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="flex items-center justify-between p-4 bg-[#0F0F1A] border-b border-gray-800">
      <div className="flex items-center gap-6">
        <Link href="/" className="text-2xl font-bold text-[#F59E0B]">Ahoum</Link>
        <Link href="/" className="hover:text-gray-300">Explore</Link>
        {user && <Link href="/dashboard" className="hover:text-gray-300">Dashboard</Link>}
        {user?.role === 'creator' && <Link href="/creator" className="hover:text-gray-300">Creator</Link>}
      </div>
      <div>
        {user ? (
          <div className="flex items-center gap-4">
            <span>{user.name || user.email}</span>
            <button onClick={logout} className="text-sm text-gray-400 hover:text-white">Logout</button>
          </div>
        ) : (
          <Link href="/auth/login" className="px-4 py-2 bg-[#F59E0B] text-black rounded hover:bg-yellow-600 font-medium">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
"""

# 4. components/SessionCard.tsx
session_card_tsx = """import Link from 'next/link';

export default function SessionCard({ session }: { session: any }) {
  return (
    <div className="border border-gray-800 rounded-lg p-4 bg-[#1a1a2e] hover:border-gray-600 transition">
      <div className="h-40 bg-gray-800 rounded-md mb-4 overflow-hidden">
        {session.image_url ? (
          <img src={session.image_url} alt={session.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-600">No Image</div>
        )}
      </div>
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-xl font-bold truncate pr-2">{session.title}</h3>
        <span className="bg-gray-800 text-xs px-2 py-1 rounded text-[#F59E0B]">{session.category}</span>
      </div>
      <p className="text-sm text-gray-400 mb-4">{session.creator_name || 'Creator'}</p>
      <div className="flex justify-between items-center text-sm">
        <span>${session.price}</span>
        <span>{session.duration} min</span>
      </div>
      <Link href={`/sessions/${session.id}`} className="mt-4 block text-center w-full py-2 bg-gray-800 hover:bg-gray-700 rounded transition">
        View Details
      </Link>
    </div>
  );
}
"""

# 5. components/LoadingSpinner.tsx
spinner_tsx = """export default function LoadingSpinner() {
  return <div className="flex justify-center p-8"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#F59E0B]"></div></div>;
}"""

# 6. components/ProtectedRoute.tsx
protected_route_tsx = """'use client';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import LoadingSpinner from './LoadingSpinner';

export default function ProtectedRoute({ children, role }: { children: React.ReactNode, role?: string }) {
  const { isAuthenticated, isLoading, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) router.push('/auth/login');
      else if (role && user?.role !== role) router.push('/dashboard');
    }
  }, [isLoading, isAuthenticated, user, role, router]);

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated || (role && user?.role !== role)) return null;

  return <>{children}</>;
}
"""

# 7. app/layout.tsx
layout_tsx = """import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { AuthProvider } from "@/lib/auth";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Ahoum Sessions Marketplace",
  description: "Find Your Inner Peace",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-[#0F0F1A] text-white min-h-screen flex flex-col`}>
        <AuthProvider>
          <Navbar />
          <main className="flex-1 max-w-7xl w-full mx-auto p-4">
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
"""

# 8. app/page.tsx
page_tsx = """'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import SessionCard from '@/components/SessionCard';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Home() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');
  
  const categories = ['All', 'Meditation', 'Yoga', 'Therapy', 'Coaching', 'Other'];

  useEffect(() => {
    setLoading(true);
    const url = category && category !== 'All' ? `/api/sessions/?category=${category}` : '/api/sessions/';
    api.get(url)
      .then(res => setSessions(res.data.results || res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [category]);

  return (
    <div>
      <div className="text-center py-16">
        <h1 className="text-5xl font-bold mb-4">Find Your Inner Peace</h1>
        <p className="text-xl text-gray-400 mb-8">Book transformative sessions with expert creators.</p>
        <div className="flex justify-center gap-4 flex-wrap">
          {categories.map(cat => (
            <button 
              key={cat} 
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-full border ${category === cat || (cat === 'All' && !category) ? 'bg-[#F59E0B] text-black border-[#F59E0B]' : 'border-gray-700 hover:border-gray-500'}`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {loading ? <LoadingSpinner /> : (
        sessions.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {sessions.map((s: any) => <SessionCard key={s.id} session={s} />)}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">No sessions found.</div>
        )
      )}
    </div>
  );
}
"""

# 9. app/auth/login/page.tsx
login_tsx = """'use client';
export default function Login() {
  const handleOAuth = (provider: string) => {
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/auth/${provider}/login/`;
  };

  return (
    <div className="flex justify-center items-center h-[70vh]">
      <div className="bg-[#1a1a2e] p-8 rounded-xl border border-gray-800 text-center w-96">
        <h1 className="text-3xl font-bold text-[#F59E0B] mb-2">Ahoum</h1>
        <p className="text-gray-400 mb-8">Sign in to book sessions</p>
        <button 
          onClick={() => handleOAuth('google')}
          className="w-full bg-white text-black py-2 rounded font-medium mb-4 hover:bg-gray-200 transition"
        >
          Continue with Google
        </button>
        <button 
          onClick={() => handleOAuth('github')}
          className="w-full bg-gray-800 text-white py-2 rounded font-medium border border-gray-700 hover:bg-gray-700 transition"
        >
          Continue with GitHub
        </button>
      </div>
    </div>
  );
}
"""

# 10. app/auth/callback/page.tsx
callback_tsx = """'use client';
import { useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter, useSearchParams } from 'next/navigation';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function AuthCallback() {
  const { login } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const access = searchParams.get('access');
    const refresh = searchParams.get('refresh');
    if (access && refresh) {
      login(access, refresh);
    } else {
      router.push('/auth/login');
    }
  }, [searchParams, login, router]);

  return <LoadingSpinner />;
}
"""

# 11. app/sessions/[id]/page.tsx
session_detail_tsx = """'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function SessionDetail({ params }: { params: { id: string } }) {
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [bookingStatus, setBookingStatus] = useState('');
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    api.get(`/api/sessions/${params.id}/`)
      .then(res => setSession(res.data))
      .catch(() => alert('Session not found'))
      .finally(() => setLoading(false));
  }, [params.id]);

  const handleBook = async () => {
    if (!isAuthenticated) {
      router.push(`/auth/login?next=/sessions/${params.id}`);
      return;
    }
    try {
      setBookingStatus('loading');
      await api.post('/api/bookings/', { session: params.id });
      setBookingStatus('booked');
    } catch (err) {
      alert('Failed to book session');
      setBookingStatus('');
    }
  };

  if (loading) return <LoadingSpinner />;
  if (!session) return <div>Not found</div>;

  return (
    <div className="max-w-3xl mx-auto py-8">
      <div className="h-64 bg-gray-800 rounded-xl mb-8 overflow-hidden">
        {session.image_url ? (
          <img src={session.image_url} alt={session.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-600">No Image provided</div>
        )}
      </div>
      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-4xl font-bold mb-2">{session.title}</h1>
          <p className="text-gray-400">by {session.creator_name || 'Creator'}</p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-[#F59E0B]">${session.price}</p>
          <p className="text-gray-400">{session.duration} mins</p>
        </div>
      </div>
      
      <div className="bg-[#1a1a2e] p-6 rounded-xl border border-gray-800 mb-8">
        <h2 className="text-xl font-bold mb-4">About this session</h2>
        <p className="text-gray-300 whitespace-pre-wrap mb-4">{session.description}</p>
        <div className="text-sm text-gray-400 space-y-2">
          <p><strong>Category:</strong> {session.category}</p>
          <p><strong>Scheduled:</strong> {new Date(session.scheduled_at || Date.now()).toLocaleString()}</p>
          <p><strong>Spots:</strong> {session.max_participants || 1}</p>
        </div>
      </div>

      <button 
        onClick={handleBook}
        disabled={bookingStatus === 'booked' || bookingStatus === 'loading'}
        className="w-full py-4 bg-[#F59E0B] text-black text-xl font-bold rounded-xl hover:bg-yellow-600 disabled:bg-green-600 disabled:text-white transition"
      >
        {bookingStatus === 'booked' ? 'Booked ✓' : bookingStatus === 'loading' ? 'Booking...' : 'Book Now'}
      </button>
    </div>
  );
}
"""

# 12. app/dashboard/page.tsx
dashboard_tsx = """'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Dashboard() {
  const [tab, setTab] = useState('bookings');
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user, setUser } = useAuth();
  
  const [formData, setFormData] = useState({ name: '', bio: '', avatar_url: '' });

  useEffect(() => {
    if (tab === 'bookings') {
      setLoading(true);
      api.get('/api/bookings/')
        .then(res => setBookings(res.data.results || res.data))
        .finally(() => setLoading(false));
    }
  }, [tab]);

  useEffect(() => {
    if (user) {
      setFormData({ name: user.name || '', bio: user.bio || '', avatar_url: user.avatar_url || '' });
    }
  }, [user]);

  const handleCancel = async (id: number) => {
    try {
      await api.patch(`/api/bookings/${id}/`, { status: 'cancelled' });
      setBookings(bookings.map((b: any) => b.id === id ? { ...b, status: 'cancelled' } : b));
    } catch (err) {
      alert('Failed to cancel');
    }
  };

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.patch('/api/users/me/', formData);
      setUser(res.data);
      alert('Profile updated');
    } catch (err) {
      alert('Update failed');
    }
  };

  const switchToCreator = async () => {
    try {
      const res = await api.patch('/api/users/me/', { role: 'creator' });
      setUser(res.data);
      alert('Switched to Creator!');
    } catch (err) {
      alert('Failed to switch role');
    }
  };

  return (
    <ProtectedRoute>
      <div className="py-8">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
        <div className="flex gap-4 mb-8 border-b border-gray-800 pb-2">
          <button onClick={() => setTab('bookings')} className={tab === 'bookings' ? 'text-[#F59E0B]' : 'text-gray-400'}>My Bookings</button>
          <button onClick={() => setTab('profile')} className={tab === 'profile' ? 'text-[#F59E0B]' : 'text-gray-400'}>Profile</button>
        </div>

        {tab === 'bookings' && (
          <div>
            {loading ? <LoadingSpinner /> : bookings.length > 0 ? (
              <div className="space-y-4">
                {bookings.map((b: any) => (
                  <div key={b.id} className="bg-[#1a1a2e] p-4 rounded border border-gray-800 flex justify-between items-center">
                    <div>
                      <h3 className="font-bold">{b.session_details?.title || 'Session'}</h3>
                      <p className="text-sm text-gray-400">Status: {b.status}</p>
                    </div>
                    {b.status !== 'cancelled' && (
                      <button onClick={() => handleCancel(b.id)} className="text-red-400 hover:text-red-300 text-sm">Cancel</button>
                    )}
                  </div>
                ))}
              </div>
            ) : <p className="text-gray-500">No bookings yet.</p>}
          </div>
        )}

        {tab === 'profile' && (
          <div className="max-w-md">
            <form onSubmit={handleProfileSave} className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Name</label>
                <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded p-2" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Bio</label>
                <textarea value={formData.bio} onChange={e => setFormData({...formData, bio: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded p-2 h-24" />
              </div>
              <button type="submit" className="bg-[#F59E0B] text-black px-4 py-2 rounded font-bold">Save Profile</button>
            </form>

            {user?.role !== 'creator' && (
              <div className="mt-12 pt-8 border-t border-gray-800">
                <h3 className="text-xl font-bold mb-2">Become a Creator</h3>
                <p className="text-sm text-gray-400 mb-4">Start hosting your own sessions and earning.</p>
                <button onClick={switchToCreator} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded border border-gray-700">Switch to Creator</button>
              </div>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
"""

# 13. app/creator/page.tsx
creator_tsx = """'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { api } from '@/lib/api';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function CreatorDashboard() {
  const [tab, setTab] = useState('sessions');
  const [sessions, setSessions] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ title: '', description: '', category: 'Meditation', price: 0, duration: 60, max_participants: 10 });

  useEffect(() => {
    fetchData();
  }, [tab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (tab === 'sessions') {
        const res = await api.get('/api/sessions/my_sessions/');
        setSessions(res.data.results || res.data);
      } else {
        const res = await api.get('/api/bookings/creator_overview/');
        setBookings(res.data.results || res.data);
      }
    } catch(err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/api/sessions/', form);
      setShowModal(false);
      fetchData();
    } catch(err) {
      alert('Failed to create');
    }
  };

  const handleDelete = async (id: number) => {
    if(confirm('Delete this session?')) {
      await api.delete(`/api/sessions/${id}/`);
      fetchData();
    }
  };

  return (
    <ProtectedRoute role="creator">
      <div className="py-8">
        <h1 className="text-3xl font-bold mb-6">Creator Dashboard</h1>
        <div className="flex gap-4 mb-8 border-b border-gray-800 pb-2">
          <button onClick={() => setTab('sessions')} className={tab === 'sessions' ? 'text-[#F59E0B]' : 'text-gray-400'}>My Sessions</button>
          <button onClick={() => setTab('bookings')} className={tab === 'bookings' ? 'text-[#F59E0B]' : 'text-gray-400'}>Booking Overview</button>
        </div>

        {tab === 'sessions' && (
          <div>
            <div className="mb-4 flex justify-end">
              <button onClick={() => setShowModal(true)} className="bg-[#F59E0B] text-black px-4 py-2 rounded font-bold">Create Session</button>
            </div>
            {loading ? <LoadingSpinner /> : (
              <div className="space-y-4">
                {sessions.map((s: any) => (
                  <div key={s.id} className="bg-[#1a1a2e] p-4 rounded border border-gray-800 flex justify-between items-center">
                    <div>
                      <h3 className="font-bold">{s.title}</h3>
                      <p className="text-sm text-gray-400">${s.price} | {s.category}</p>
                    </div>
                    <div>
                      <button onClick={() => handleDelete(s.id)} className="text-red-400 hover:text-red-300 text-sm">Delete</button>
                    </div>
                  </div>
                ))}
                {sessions.length === 0 && <p className="text-gray-500">No sessions created yet.</p>}
              </div>
            )}
          </div>
        )}

        {tab === 'bookings' && (
          <div>
            {loading ? <LoadingSpinner /> : (
              <div className="space-y-4">
                {bookings.map((b: any) => (
                  <div key={b.id} className="bg-[#1a1a2e] p-4 rounded border border-gray-800">
                    <h3 className="font-bold">Booking #{b.id} - {b.status}</h3>
                    <p className="text-sm text-gray-400">User: {b.user_details?.name || b.user_details?.email}</p>
                    <p className="text-sm text-gray-400">Session: {b.session_details?.title}</p>
                  </div>
                ))}
                {bookings.length === 0 && <p className="text-gray-500">No bookings yet.</p>}
              </div>
            )}
          </div>
        )}

        {showModal && (
          <div className="fixed inset-0 bg-black/80 flex justify-center items-center p-4">
            <div className="bg-[#1a1a2e] p-6 rounded-xl border border-gray-800 w-full max-w-md">
              <h2 className="text-2xl font-bold mb-4">Create Session</h2>
              <form onSubmit={handleCreate} className="space-y-4">
                <input placeholder="Title" required value={form.title} onChange={e => setForm({...form, title: e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <textarea placeholder="Description" required value={form.description} onChange={e => setForm({...form, description: e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <input type="number" placeholder="Price" required value={form.price} onChange={e => setForm({...form, price: +e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <input type="number" placeholder="Duration (min)" required value={form.duration} onChange={e => setForm({...form, duration: +e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <div className="flex gap-4">
                  <button type="button" onClick={() => setShowModal(false)} className="w-full py-2 bg-gray-800 rounded">Cancel</button>
                  <button type="submit" className="w-full py-2 bg-[#F59E0B] text-black rounded font-bold">Create</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
"""

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

write_file(os.path.join(lib_dir, "api.ts"), api_ts)
write_file(os.path.join(lib_dir, "auth.tsx"), auth_tsx)
write_file(os.path.join(components_dir, "Navbar.tsx"), navbar_tsx)
write_file(os.path.join(components_dir, "SessionCard.tsx"), session_card_tsx)
write_file(os.path.join(components_dir, "LoadingSpinner.tsx"), spinner_tsx)
write_file(os.path.join(components_dir, "ProtectedRoute.tsx"), protected_route_tsx)
write_file(os.path.join(app_dir, "layout.tsx"), layout_tsx)
write_file(os.path.join(app_dir, "page.tsx"), page_tsx)
write_file(os.path.join(app_dir, "auth", "login", "page.tsx"), login_tsx)
write_file(os.path.join(app_dir, "auth", "callback", "page.tsx"), callback_tsx)
write_file(os.path.join(app_dir, "sessions", "[id]", "page.tsx"), session_detail_tsx)
write_file(os.path.join(app_dir, "dashboard", "page.tsx"), dashboard_tsx)
write_file(os.path.join(app_dir, "creator", "page.tsx"), creator_tsx)
