"use client";

import { IconDotsVertical } from "@tabler/icons-react";
import { CircleUser, LogIn, LogOut } from "lucide-react";
import { ErrorItem } from "@/components/common/ErrorItem";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSkeleton,
  useSidebar,
} from "@/components/ui/sidebar";
import { useUserData } from "@/hooks/useUserData";
import { api } from "@/lib/client";
import { GOOGLE_AUTH_PATH, LOGOUT_PATH } from "@/lib/constants";
import { formatTimestamp } from "@/lib/utils";
import { LorestoneBalance } from "./LorestoneBalance";

export function NavUser() {
  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <Content />
      </SidebarMenuItem>
    </SidebarMenu>
  );
}

const Content = () => {
  const { isMobile } = useSidebar();
  const {
    data: userData,
    isPending: userDataIsPending,
    error: userDataError,
    isFetching: userDataIsFetching,
    refetch: refetchUserData,
  } = useUserData();
  const healthcheck = api.useQuery("get", "/v1/healthz");
  if (userDataIsPending) return <SidebarMenuSkeleton showIcon />;

  if (userDataError) {
    if (userDataError.status_code === 401) {
      return (
        <SidebarMenuButton asChild>
          <Button asChild>
            <a href={GOOGLE_AUTH_PATH}>
              <LogIn /> Login
            </a>
          </Button>
        </SidebarMenuButton>
      );
    }
    return (
      <ErrorItem
        message="Error fetching user data"
        isFetching={userDataIsFetching}
        refetch={refetchUserData}
      />
    );
  }

  return (
    <Dialog>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <SidebarMenuButton
            size="lg"
            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground max-w-full"
          >
            <Avatar className="h-8 w-8 rounded-lg grayscale">
              <AvatarImage src={userData.picture ?? ""} />
              <AvatarFallback className="rounded-lg">
                {userData.name?.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="flex flex-col flex-1 min-w-0 text-left text-sm leading-tight">
              <span className="truncate font-medium">{userData.name}</span>
              <LorestoneBalance />
            </div>
            <IconDotsVertical className="ml-auto size-4" />
          </SidebarMenuButton>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
          side={isMobile ? "bottom" : "right"}
          align="end"
          sideOffset={4}
        >
          <DropdownMenuGroup>
            <DropdownMenuItem className="opacity-50">
              <CircleUser />
              <span className="truncate">{userData.email}</span>
            </DropdownMenuItem>
            <DialogTrigger asChild>
              <DropdownMenuItem>Version Info</DropdownMenuItem>
            </DialogTrigger>
            <DropdownMenuItem asChild className="cursor-pointer">
              <a href={LOGOUT_PATH}>
                <LogOut />
                Log out
              </a>
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Version Info</DialogTitle>
          <DialogDescription>
            {healthcheck.error ? (
              "Error fetching version info"
            ) : healthcheck.isPending ? (
              "Loading..."
            ) : (
              <>
                Commit SHA: {healthcheck.data.commit_sha}
                <br />
                {formatTimestamp(healthcheck.data.commit_timestamp * 1000)}
                <br />
                Environment: {healthcheck.data.environment}
                <br />
              </>
            )}
          </DialogDescription>
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
};
