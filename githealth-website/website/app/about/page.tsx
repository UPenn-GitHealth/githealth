import React from "react";
import Image from "next/image";
import Header from '../components/Header';

const teamMembers = [
  { name: "Riju Datta", title: "Role or Title", imageSrc: "/headshots/riju.png", description: "CIS Senior" },
  { name: "Zain Khan", title: "Role or Title", imageSrc: "/headshots/zain.jpg", description: "CIS Senior" },
  { name: "Anshul Sukhlecha", title: "Role or Title", imageSrc: "/headshots/anshul.jpg", description: "CIS Senior" },
  { name: "George Wang", title: "Role or Title", imageSrc: "/headshots/george.jpg", description: "CIS Senior" },
  { name: "Valery Yakubovich", title: "Role or Title", imageSrc: "/headshots/valery.jpg", description: "Executive Director of Mack Institute" },
  { name: "Soumya Dash", title: "Role or Title", imageSrc: "/headshots/soumya.jpg", description: "Master's Student" },
  { name: "Rahul Mangharam", title: "Role or Title", imageSrc: "/headshots/rahul.jpg", description: "ESE Associate Professor" },
  { name: "Patricia Gruver-Barr", title: "Role or Title", imageSrc: "/headshots/patricia.png", description: "Associate Director of Innovation Ecosystems at Mack Institute" },
  { name: "Bharath Teegala", title: "Role or Title", imageSrc: "/headshots/bharath.jpg", description: "Teaching Assistant" }

];

const About = () => {
    return (
        <div className="bg-gray-100 min-h-screen flex flex-col">
            <Header />
            <div className="max-w-5xl mx-auto p-8">
                <h1 className="text-3xl text-black font-bold text-center mb-12">About Our Team</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {teamMembers.map((member, index) => (
                        <div key={index} className="flex flex-col items-center text-center mb-8">
                            <div className="w-48 h-48 mb-4">
                                <Image
                                    src={member.imageSrc}
                                    alt={member.name}
                                    width={192}
                                    height={192}
                                    className="rounded-full"
                                />
                            </div>
                            <h2 className="text-xl text-black font-semibold">{member.name}</h2>
                            <p className="text-black mt-2">{member.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default About;
