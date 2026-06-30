'use client';
export default function Login() {
  const handleOAuth = (provider: string) => {
    const redirectUri = `${window.location.origin}/auth/callback`;
    if (provider === 'google') {
      const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || 'mock_client_id';
      window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=email profile&state=google`;
    } else if (provider === 'github') {
      const clientId = process.env.NEXT_PUBLIC_GITHUB_CLIENT_ID || 'mock_client_id';
      window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user:email&state=github`;
    }
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
