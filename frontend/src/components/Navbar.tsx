'use client';
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
