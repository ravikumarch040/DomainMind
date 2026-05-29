import { COMPANY_NAME, CONTACT_EMAIL, demoMailto, navLinks, PRODUCT_NAME } from "../content/site";

export default function Footer() {
  return (
    <footer className="border-t border-slate-700 bg-marketing-dark py-12 text-slate-300">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid gap-10 md:grid-cols-3">
          <div>
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-marketing-accent">
                <span className="text-sm font-bold text-white">D</span>
              </div>
              <span className="font-serif text-xl text-white">{PRODUCT_NAME}</span>
            </div>
            <p className="mt-2 text-sm text-slate-400">by {COMPANY_NAME}</p>
            <p className="mt-4 text-sm">
              Compliance AI for regulated organizations.
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">Navigate</h3>
            <ul className="mt-4 space-y-2">
              {navLinks.map((link) => (
                <li key={link.href}>
                  <a href={link.href} className="text-sm transition hover:text-white">
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">Contact</h3>
            <p className="mt-4">
              <a href={demoMailto} className="text-sm text-marketing-gold transition hover:text-white">
                {CONTACT_EMAIL}
              </a>
            </p>
            <div className="mt-4 flex gap-4 text-sm text-slate-500">
              <a href="#" className="transition hover:text-slate-300">
                Privacy Policy
              </a>
              <a href="#" className="transition hover:text-slate-300">
                Terms
              </a>
            </div>
          </div>
        </div>

        <div className="mt-10 border-t border-slate-700 pt-6 text-center text-sm text-slate-500">
          © {new Date().getFullYear()} {COMPANY_NAME}. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
