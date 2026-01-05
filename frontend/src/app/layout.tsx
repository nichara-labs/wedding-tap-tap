import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Tapping Game",
  description: "Groom vs Bride tapping game",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
