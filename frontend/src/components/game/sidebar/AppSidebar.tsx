"use client";
import { PanelLeftIcon, X } from "lucide-react";
import { NavChats } from "@/components/game/sidebar/NavChats";
import { NavMain } from "@/components/game/sidebar/NavMain";
import { NavUser } from "@/components/game/sidebar/NavUser";
import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarSeparator,
  useSidebar,
} from "@/components/ui/sidebar";
import { useIsMobile } from "@/hooks/use-mobile";
import { cn } from "@/lib/utils";
import { ClaimDailyLorestones } from "./ClaimDailyLorestones";
import { DarkModeToggle } from "./DarkModeToggle";
import { LogoButton } from "./LogoButton";

export function AppSidebar({
  className,
  variant,
  ...props
}: React.ComponentPropsWithoutRef<typeof Sidebar>) {
  const { open, toggleSidebar } = useSidebar();
  const isMobile = useIsMobile();

  return (
    <Sidebar
      collapsible="icon"
      variant={variant}
      className={cn("group/sidebar", !open && "cursor-e-resize", className)}
      onClick={!open ? toggleSidebar : undefined}
      {...props}
    >
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem className="flex items-center">
            <LogoButton className="mr-2" />
            {open && (
              <div className="flex items-center justify-between flex-1">
                <h1 className="font-stylish text-2xl whitespace-nowrap overflow-clip">
                  Forgotten Tome
                </h1>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={toggleSidebar}
                  className="cursor-w-resize"
                >
                  <X className="md:hidden" aria-hidden />
                  <PanelLeftIcon className="hidden md:block" aria-hidden />
                </Button>
              </div>
            )}
          </SidebarMenuItem>
        </SidebarMenu>
        {!isMobile && <NavMain />}
      </SidebarHeader>
      <SidebarContent>
        {isMobile && <NavMain />}
        <NavChats />
      </SidebarContent>
      <SidebarSeparator />
      <SidebarFooter>
        <ClaimDailyLorestones />
        <DarkModeToggle />
        <NavUser />
      </SidebarFooter>
    </Sidebar>
  );
}
