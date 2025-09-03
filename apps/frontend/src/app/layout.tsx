import type { Metadata } from "next";
import { Inter, Raleway } from "next/font/google";
import "./globals.css";

// Configure the body font (Inter)
const fontSans = Inter({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-sans",
});

// Configure the headline font (Raleway)
const fontHeadline = Raleway({
  subsets: ["latin"],
  weight: ["600", "700"],
  variable: "--font-headline",
});

export const metadata: Metadata = {
  title: "Project Phoenix",
  description: "AI-Enhanced Autonomous Content Pipeline",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${fontSans.variable} ${fontHeadline.variable}`}>
        {children}
      </body>
    </html>
  );
}