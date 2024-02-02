import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

const Header = () => {
  return (
    <header className="w-full flex justify-start items-center bg-white shadow-md px-5 py-3">
      <Link href="/" passHref>
        <div className="flex items-center cursor-pointer">
          <Image
            src="/GitHealth_Logo.jpeg"
            alt="GitHealth Logo"
            width={100}
            height={100}
          />
          <span className="ml-3 text-xl font-bold">GitHealth</span>
        </div>
      </Link>
      {/* <h1 className="text-xl font-bold text-center flex-grow">
        <span className="text-gray-900">Welcome to GitHealth!</span>
      </h1> */}
      <nav className="ml-auto">
        <ul className="flex space-x-4">
          <li>  
            <Link href="/">
                <span className="text-blue-600 hover:text-blue-700">Home</span>
            </Link>
          </li>
          <li>
            <Link href="/metrics">
                <span className="text-blue-600 hover:text-blue-700">Metrics</span>
            </Link>
          </li>
          <li>
            <Link href="/about">
                <span className="text-blue-600 hover:text-blue-700">About</span>
            </Link>
          </li>
          <li>
            <Link href="/contact">
                <span className="text-blue-600 hover:text-blue-700">Contact Us</span>
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
