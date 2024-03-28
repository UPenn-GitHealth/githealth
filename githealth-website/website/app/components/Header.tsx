"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="w-full flex justify-start items-center shadow-md px-5 py-3"
      style={{ background: 'linear-gradient(to right, #00B4DB, #09b50c)' }}
    >
      <Link href="/" passHref>
        <div className="flex items-center cursor-pointer">
          <Image
            src="/GitHealth_Logo.jpeg"
            alt="GitHealth Logo"
            width={100}
            height={100}
          />
        </div>
      </Link>
      <nav className="ml-auto">
        <ul className="flex space-x-4">
          <li>  
            <Link href="/">
                <span className="text-white hover:text-gray-300">Home</span>
            </Link>
          </li>
          <li className="relative">
            <button 
              className="text-white hover:text-gray-300 focus:outline-none flex items-center" 
              onClick={() => setIsOpen(!isOpen)}
            >
              Metrics <span className="ml-1">&#9660;</span>
            </button>
            {isOpen && (
              <ul className="absolute bg-white shadow-lg rounded mt-2 py-1 w-40 right-0 z-10"> {/* Added z-10 here */}
                <li className="px-4 py-2 hover:bg-gray-100">
                  <Link href="/issues">
                    <span className="text-black">Issues</span>
                  </Link>
                </li>
                <li className="px-4 py-2 hover:bg-gray-100">
                  <Link href="/discussions">
                    <span className="text-black">Discussions</span>
                  </Link>
                </li>
                <li className="px-4 py-2 hover:bg-gray-100">
                  <Link href="/users">
                    <span className="text-black">Users</span>
                  </Link>
                </li>
                <li className="px-4 py-2 hover:bg-gray-100">
                  <Link href="/organizations">
                    <span className="text-black">Organizations</span>
                  </Link>
                </li>
              </ul>
            )}
          </li>
          <li>
            <Link href="/about">
                <span className="text-white hover:text-gray-300">About</span>
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
