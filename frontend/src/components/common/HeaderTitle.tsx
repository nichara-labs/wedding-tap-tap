import type { PropsWithChildren } from "react";

export const HeaderTitle = ({ children }: PropsWithChildren) => (
  <h1 className="text-base font-medium min-w-0 truncate">{children}</h1>
);
