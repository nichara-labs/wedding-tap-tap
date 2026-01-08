import type { Metadata } from "next";
import { Provider } from "@/components/Provider";
import { Toaster } from "@/components/ui/sonner";
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
      <Provider>
        <body>{children}</body>
      </Provider>
      <Toaster />
    </html>
  );
}
