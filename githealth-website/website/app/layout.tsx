import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
<<<<<<< HEAD
  title: 'GitHealth',
  description: 'Autoware Analysis',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
=======
    title: 'GitHealth',
    description: 'Autoware Analysis',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>{children}</body>
        </html>
    )
>>>>>>> 5d86f957e2057247185e05933af4b8a8ee305b31
}
