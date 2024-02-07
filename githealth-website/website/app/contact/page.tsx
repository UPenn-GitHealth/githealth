import React from "react";
import Header from '../components/Header';

const ContactUs = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <div className="max-w-4xl mx-auto p-8">
                <h1 className="text-3xl text-black font-bold text-center mb-6">Contact Us</h1>
                <p className="text-center text-black mb-8">
                    If you have any questions or would like more information, please contact us using the form below.
                </p>
                <form className="space-y-6">
                    <div>
                        <label htmlFor="name" className="text-sm font-medium text-gray-900 block mb-2">Your Name</label>
                        <input type="text" id="name" name="name" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="Zain Khan" required />
                    </div>
                    <div>
                        <label htmlFor="email" className="text-sm font-medium text-gray-900 block mb-2">Your Email</label>
                        <input type="email" id="email" name="email" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="zainkhan@example.com" required />
                    </div>
                    <div>
                        <label htmlFor="message" className="text-sm font-medium text-gray-900 block mb-2">Your Message</label>
                        <textarea id="message" name="message" rows={4} className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="Your message..." required></textarea>
                    </div>
                    <button type="submit" className="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center">Submit</button>
                </form>
            </div >
        </div >
    );
};

export default ContactUs;
