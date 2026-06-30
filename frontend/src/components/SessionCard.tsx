import Link from 'next/link';

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
