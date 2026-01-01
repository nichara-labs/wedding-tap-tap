import { GoogleTagManager } from "@next/third-parties/google";
import type { Metadata } from "next";
import { Metal_Mania, Nunito, PT_Serif } from "next/font/google";
import { Providers } from "@/components/Providers";
import { Toaster } from "@/components/ui/sonner";
import { settings } from "@/lib/settings";
import { cn } from "@/lib/utils";
import "./globals.css";
export const metadata: Metadata = {
  title: "Forgotten Tome | Forge Your Adventure",
  description:
    "Guide your party, manage subscriptions, and stay immersed in your Forgotten Tome adventures from the live story console.",
};

const stylish = Metal_Mania({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-metal-mania",
});

const nunito = Nunito({
  subsets: ["latin"],
  variable: "--font-nunito",
});

const ptSerif = PT_Serif({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-pt-serif",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={cn(stylish.variable, nunito.variable, ptSerif.variable)}
      suppressHydrationWarning
      data-scroll-behavior="smooth"
    >
      <GoogleTagManager
        gtmId={settings.gtm_id}
        gtmScriptUrl={settings.gt_gateway_path}
      />
      <body>
        <Providers attribute="class" enableSystem disableTransitionOnChange>
          {children}
        </Providers>
        <div className="texture" />
        <Toaster richColors position="top-center" closeButton />
      </body>
    </html>
  );
}
