import type { ReactElement, ReactNode } from "react";
import { create } from "zustand";
import { HeaderTitle } from "@/components/common/HeaderTitle";

interface State {
  jsx: ReactNode;
  setHeader: (jsx: ReactElement) => void;
  setHeaderText: (header: string) => void;
}

export const useStore = create<State>((set) => ({
  jsx: <HeaderTitle>Forgotten Tome</HeaderTitle>,
  setHeader: (jsx: ReactElement) => set(() => ({ jsx })),
  setHeaderText: (header: string) =>
    set(() => ({ jsx: <HeaderTitle>{header}</HeaderTitle> })),
}));
