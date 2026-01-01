"use client";
import { LogIn, Menu } from "lucide-react";
import { useSidebar } from "@/components/ui/sidebar";
import { useUserData } from "@/hooks/useUserData";
import { GOOGLE_AUTH_PATH } from "@/lib/constants";
import { useStore } from "@/lib/store";
import { Button } from "../ui/button";

export const Header = () => {
  const { toggleSidebar } = useSidebar();
  const { data: userData, isPending: userDataPending } = useUserData();
  const headerJsx = useStore((state) => state.jsx);

  return (
    <header className="sticky top-0 backdrop-blur-xs bg-background/80 flex h-(--header-height) shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height) truncate">
      <div className="flex items-center md:justify-center w-full gap-1 px-1 lg:gap-2 md:px-4">
        <Button
          onClick={toggleSidebar}
          variant="ghost"
          size="icon"
          className="md:hidden"
        >
          <Menu />
        </Button>
        {headerJsx}
        {!userDataPending && !userData && (
          <Button asChild>
            <a href={GOOGLE_AUTH_PATH}>
              <LogIn />
              Login
            </a>
          </Button>
        )}
      </div>
    </header>
  );
};
