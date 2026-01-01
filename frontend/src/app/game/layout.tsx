import type { Viewport } from "next";
import { Header } from "@/components/game/Header";
import { AppSidebar } from "@/components/game/sidebar/AppSidebar";
import { SidebarProvider } from "@/components/ui/sidebar";

export const viewport: Viewport = {
  /* Causes the viewport to shrink when the mobile keyboard is open, ensuring the Composer is always visible.
  https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport#interactive-widget */
  interactiveWidget: "resizes-content",
};

export default function GameLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SidebarProvider>
      <AppSidebar variant="sidebar" />
      <main className="w-full px-4">
        <Header />
        {children}
      </main>
    </SidebarProvider>
  );
}
