"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Logo } from "../common/Logo";

const navItems = [
  { href: "/#realms", label: "Realms" },
  { href: "/#features", label: "Features" },
  { href: "/#community", label: "Community" },
] as const;

export const Header = () => {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-[#070212]/80 backdrop-blur-lg">
      <div className="container mx-auto flex items-center justify-between px-4 py-3">
        <Link href="/" className="flex items-center gap-3">
          <Logo />
          <span className="text-2xl font-semibold font-stylish tracking-wide text-white drop-shadow-[0_2px_12px_rgba(148,113,255,0.6)]">
            Forgotten Tome
          </span>
        </Link>
        <nav className="hidden items-center gap-1 md:flex">
          {navItems.map((item) => (
            <Button key={item.href} variant="ghost" size="sm" asChild>
              <Link
                href={item.href}
                className="text-sm font-medium tracking-wide text-slate-200"
              >
                {item.label}
              </Link>
            </Button>
          ))}
        </nav>
      </div>
    </header>
  );
};
