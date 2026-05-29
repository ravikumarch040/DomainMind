import { demoMailto, navLinks, PRODUCT_NAME } from "../content/site";

interface NavbarProps {
  mobileOpen: boolean;
  onToggle: () => void;
}

export default function Navbar({ mobileOpen, onToggle }: NavbarProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-marketing-border bg-marketing-surface/95 backdrop-blur-sm">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <a href="#" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-marketing-dark">
            <span className="text-sm font-bold text-marketing-accent">D</span>
          </div>
          <span className="font-serif text-xl text-marketing-text">{PRODUCT_NAME}</span>
        </a>

        <nav className="hidden items-center gap-8 lg:flex">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-marketing-muted transition hover:text-marketing-accent"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <a
            href={demoMailto}
            className="hidden rounded-lg bg-marketing-accent px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700 sm:inline-block"
          >
            Request a demo
          </a>
          <button
            type="button"
            onClick={onToggle}
            className="rounded-lg p-2 text-marketing-text lg:hidden"
            aria-label="Toggle menu"
            aria-expanded={mobileOpen}
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav className="border-t border-marketing-border bg-marketing-surface px-6 py-4 lg:hidden">
          <div className="flex flex-col gap-3">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                onClick={onToggle}
                className="text-sm font-medium text-marketing-muted transition hover:text-marketing-accent"
              >
                {link.label}
              </a>
            ))}
            <a
              href={demoMailto}
              className="mt-2 rounded-lg bg-marketing-accent px-4 py-2 text-center text-sm font-semibold text-white"
            >
              Request a demo
            </a>
          </div>
        </nav>
      )}
    </header>
  );
}
