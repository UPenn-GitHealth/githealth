/** @type {import('next').NextConfig} */
const PRODUCTION_API_DOMAIN = "https://githealth-backend-j6sy.onrender.com/";
const nextConfig = {
    rewrites: async () => {
        return [
            {
                source: "/api/:path*",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/:path*"
                        : PRODUCTION_API_DOMAIN + ":path*",
            },
            {
                source: "/docs",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/docs"
                        : "/api/docs",
            },
            {
                source: "/openapi.json",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/openapi.json"
                        : "/api/openapi.json",
            },
        ];
    },
};

module.exports = nextConfig;
