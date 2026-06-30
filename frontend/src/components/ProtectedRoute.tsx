'use client';
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
