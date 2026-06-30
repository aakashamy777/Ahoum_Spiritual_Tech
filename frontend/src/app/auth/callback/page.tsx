'use client';
import { useEffect, Suspense } from 'react';
import { useAuth } from '@/lib/auth';
import { useRouter, useSearchParams } from 'next/navigation';
import LoadingSpinner from '@/components/LoadingSpinner';
import { api } from '@/lib/api';

function CallbackContent() {
  const { login } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const code = searchParams.get('code');
    const state = searchParams.get('state'); // 'google' or 'github'
    
    // Check if this is a standard callback with direct tokens
    const access = searchParams.get('access');
    const refresh = searchParams.get('refresh');
    
    if (access && refresh) {
      login(access, refresh);
      return;
    }
    
    if (code && state) {
      api.post(`/api/auth/${state}/`, { 
        code, 
        redirect_uri: `${window.location.origin}/auth/callback` 
      })
      .then(res => {
        if (res.data.access && res.data.refresh) {
          login(res.data.access, res.data.refresh);
        } else {
          router.push('/auth/login?error=InvalidToken');
        }
      })
      .catch(err => {
        console.error('OAuth exchange error', err);
        router.push('/auth/login?error=OAuthFailed');
      });
    } else {
      router.push('/auth/login');
    }
  }, [searchParams, login, router]);

  return <LoadingSpinner />;
}

export default function AuthCallback() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <CallbackContent />
    </Suspense>
  );
}
