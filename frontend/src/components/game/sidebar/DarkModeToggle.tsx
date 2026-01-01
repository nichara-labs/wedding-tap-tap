import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";

export const DarkModeToggle = () => {
  const { resolvedTheme, setTheme } = useTheme();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  const handleToggle = () => {
    setTheme(resolvedTheme === "dark" ? "light" : "dark");
  };

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton onClick={handleToggle} tooltip={"Change Theme"}>
          {isClient && resolvedTheme === "dark" ? <Moon /> : <Sun />}
          Change Theme
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  );
};
