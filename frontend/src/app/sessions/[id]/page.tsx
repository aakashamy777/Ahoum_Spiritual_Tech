'use client';
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
