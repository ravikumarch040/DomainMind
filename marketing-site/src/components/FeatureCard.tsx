interface FeatureCardProps {
  title: string;
  description: string;
}

export default function FeatureCard({ title, description }: FeatureCardProps) {
  return (
    <div className="rounded-2xl border border-marketing-border bg-marketing-surface p-6 shadow-sm transition hover:shadow-md">
      <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-lg bg-marketing-accent/10">
        <div className="h-2 w-2 rounded-full bg-marketing-accent" />
      </div>
      <h3 className="font-semibold text-marketing-text">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-marketing-muted">{description}</p>
    </div>
  );
}
