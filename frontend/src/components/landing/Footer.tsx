import Link from "next/link";

export const Footer = () => {
  return (
    <footer className="mt-20 border-t border-white/10 bg-[#05020f] py-10">
      <div className="container mx-auto flex flex-col items-center gap-4 px-4 text-center text-sm text-slate-300">
        <p className="text-base font-medium text-slate-200">
          © {new Date().getFullYear()} Forgotten Tome. May your adventures be
          legendary.
        </p>
        <nav
          className="flex flex-wrap items-center justify-center gap-3"
          aria-label="Footer"
        >
          <Link
            href="/terms"
            className="transition-colors hover:text-violet-200"
          >
            Terms
          </Link>
          <span className="text-slate-500">•</span>
          <Link
            href="/privacy"
            className="transition-colors hover:text-violet-200"
          >
            Privacy
          </Link>
          <span className="text-slate-500">•</span>
          <Link
            href="/refund"
            className="transition-colors hover:text-violet-200"
          >
            Refund
          </Link>
          <span className="text-slate-500">•</span>
          <Link
            href="mailto:hello@forgottentome.com"
            className="transition-colors hover:text-violet-200"
          >
            Reach the Guild
          </Link>
        </nav>
      </div>
    </footer>
  );
};
