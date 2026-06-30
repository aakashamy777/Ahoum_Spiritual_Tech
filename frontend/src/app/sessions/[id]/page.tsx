'use client';

import { useState } from 'react';

// Next.js page mockup for Session Detail + Razorpay + Toast
export default function SessionDetail({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(false);
  
  // Dummy session data (usually fetched from API)
  const session = {
    id: params.id,
    title: 'Yoga Mastery',
    price: 500, // INR
  };

  const handleBooking = async () => {
    setLoading(true);
    try {
      // 1. Create order
      const res = await fetch('/api/payments/create-order/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: session.id })
      });

      if (res.status === 429) {
        alert('Toast: Rate limit exceeded, try again in a few seconds');
        setLoading(false);
        return;
      }

      const data = await res.json();

      if (session.price > 0) {
        // 2. Load Razorpay
        const options = {
          key: data.key,
          amount: data.amount,
          currency: data.currency,
          name: 'Ahoum Sessions',
          description: session.title,
          order_id: data.order_id,
          handler: async function (response: any) {
            // 3. Verify
            const verifyRes = await fetch('/api/payments/verify/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_signature: response.razorpay_signature,
                booking_id: data.booking_id,
              })
            });
            if (verifyRes.ok) alert('Payment Successful! Booking confirmed.');
          },
        };
        const rzp = new (window as any).Razorpay(options);
        rzp.open();
      } else {
        alert('Booking confirmed (Free session).');
      }
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="p-8">
      {/* Must include razorpay script in real app, often in _document.tsx or next/script */}
      <script src="https://checkout.razorpay.com/v1/checkout.js" async></script>
      <h1 className="text-3xl font-bold">{session.title}</h1>
      <p className="mt-2 text-lg">Price: ₹{session.price}</p>
      
      <button 
        onClick={handleBooking}
        disabled={loading}
        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded"
      >
        {session.price > 0 ? 'Pay & Book' : 'Book Now'}
      </button>
    </div>
  );
}
