import { ReactNode } from "react";

interface SectionProps {
  id?: string;
  title?: string;
  subtitle?: string;
  children: ReactNode;
  dark?: boolean;
  className?: string;
}

export default function Section({ id, title, subtitle, children, dark, className = "" }: SectionProps) {
  return (
    <section
      id={id}
      className={`py-20 md:py-24 ${dark ? "bg-marketing-dark text-white" : ""} ${className}`}
    >
      <div className="mx-auto max-w-6xl px-6">
        {(title || subtitle) && (
          <div className="mb-12 max-w-2xl">
            {title && (
              <h2 className={`font-serif text-3xl md:text-4xl ${dark ? "text-white" : "text-marketing-text"}`}>
                {title}
              </h2>
            )}
            {subtitle && (
              <p className={`mt-4 text-lg ${dark ? "text-slate-300" : "text-marketing-muted"}`}>{subtitle}</p>
            )}
          </div>
        )}
        {children}
      </div>
    </section>
  );
}
