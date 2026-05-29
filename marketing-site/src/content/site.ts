export const CONTACT_EMAIL = "ravindrakumarch@outlook.com";
export const COMPANY_NAME = "RK iTech Solutions";
export const PRODUCT_NAME = "DomainMind";

export const demoMailto = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent("DomainMind Demo Request")}`;

export const navLinks = [
  { label: "Why DomainMind", href: "#why" },
  { label: "How it works", href: "#how-it-works" },
  { label: "Features", href: "#features" },
  { label: "Use cases", href: "#use-cases" },
  { label: "Security", href: "#security" },
  { label: "FAQ", href: "#faq" },
];

export const hero = {
  headline: "Compliance answers you can trust — backed by your documents.",
  subhead:
    "Built for compliance officers and risk teams. DomainMind combines domain-trained AI with your policy library so you get fast, cited answers on SOC 2, HIPAA, and HITECH — without hunting through PDFs.",
  primaryCta: "Request a demo",
  secondaryCta: "See how it works",
};

export const problem = {
  title: "Why regulated teams can't use generic AI",
  subtitle: "Public chatbots weren't built for audit-ready compliance work.",
  cards: [
    {
      title: "Inconsistent answers",
      description: "Generic AI doesn't know your policies. Different team members get different guidance.",
    },
    {
      title: "No audit trail",
      description: "Hard to verify where an answer came from when an auditor asks for proof.",
    },
    {
      title: "Compliance risk",
      description: "Sensitive data and regulatory expectations require more than a public chatbot.",
    },
  ],
};

export const howItWorks = {
  title: "How it works",
  subtitle: "Three simple steps to trustworthy compliance answers.",
  steps: [
    {
      step: "1",
      title: "Upload your documents",
      description: "Policies, procedures, and compliance materials — PDF or Word.",
    },
    {
      step: "2",
      title: "Ask in plain language",
      description: '"What are our HIPAA breach notification steps?"',
    },
    {
      step: "3",
      title: "Get cited answers",
      description: "AI responds with links to the exact source passages in your documents.",
    },
  ],
  reassurance: "Your data stays isolated. Your team stays in control.",
};

export const features = {
  title: "Everything you need for compliance Q&A",
  subtitle: "Purpose-built capabilities that generic AI tools can't match.",
  items: [
    {
      title: "Cited answers",
      description: "Verify every response against your documents — not guesses from the open internet.",
    },
    {
      title: "Domain-trained AI",
      description: "Understands compliance language on SOC 2, HIPAA, and HITECH out of the box.",
    },
    {
      title: "Document library",
      description: "Keep your knowledge base current with easy PDF and DOCX uploads.",
    },
    {
      title: "Quality dashboard",
      description: "Measure accuracy before rolling out to the whole team.",
    },
    {
      title: "Multi-tenant security",
      description: "Separate environments for each customer — your data never mixes with others.",
    },
    {
      title: "Enterprise-ready",
      description: "Encryption, access controls, and audit-friendly logging built in.",
    },
  ],
};

export const useCases = {
  title: "Built for the teams who need it most",
  subtitle: "From daily policy questions to audit prep.",
  items: [
    {
      role: "Compliance officer",
      badge: "Primary",
      description: "Instant policy lookup during audits. Defend every answer with source citations.",
    },
    {
      role: "Risk manager",
      description: "Consistent SOC 2 and HIPAA guidance across the organization.",
    },
    {
      role: "Privacy / legal team",
      description: "Interpret regulations against your internal standards — quickly and consistently.",
    },
    {
      role: "Security leader",
      description: "Evaluate AI that meets your isolation and encryption requirements.",
    },
  ],
};

export const security = {
  title: "Security & compliance",
  subtitle: "Designed for regulated environments from day one.",
  items: [
    "Designed for HIPAA and SOC 2 aligned workloads",
    "Data encrypted at rest; private network architecture",
    "Sensitive information scrubbed from training pipelines",
    "Per-customer data isolation",
    "Access controls and API key management",
    "Audit logging for accountability",
  ],
  disclaimer:
    "Compliance is a shared responsibility. DomainMind provides controls aligned with common regulatory frameworks.",
};

export const comparison = {
  title: "Why DomainMind",
  subtitle: "See how we compare to generic AI tools.",
  genericLabel: "Generic AI",
  domainMindLabel: "DomainMind",
  rows: [
    { generic: "General knowledge", domainMind: "Compliance-focused" },
    { generic: "No source citations", domainMind: "Cited document references" },
    { generic: "Unknown quality", domainMind: "Built-in quality measurement" },
    { generic: "Shared public model", domainMind: "Isolated tenant environment" },
  ],
};

export const faq = {
  title: "Frequently asked questions",
  items: [
    {
      q: "What is DomainMind?",
      a: "DomainMind is an AI platform built for compliance and legal teams. It combines domain-trained AI with your own document library to deliver fast, cited answers about SOC 2, HIPAA, HITECH, and related frameworks.",
    },
    {
      q: "Who is it for?",
      a: "Compliance officers, risk managers, privacy and legal teams, and security leaders at regulated organizations — healthcare providers, fintech firms, and SaaS vendors pursuing SOC 2.",
    },
    {
      q: "How is this different from ChatGPT?",
      a: "DomainMind is trained for compliance topics, searches your own policies for every answer, and cites the source documents. It also includes built-in quality measurement and enterprise security controls generic chatbots lack.",
    },
    {
      q: "Can we use our own documents?",
      a: "Yes. Upload PDF and DOCX files to build your knowledge base. Every answer can reference the exact passages in your uploaded materials.",
    },
    {
      q: "Is it secure enough for regulated data?",
      a: "DomainMind is designed for HIPAA and SOC 2 aligned workloads with encryption at rest, per-customer data isolation, access controls, and audit logging.",
    },
    {
      q: "How do you measure answer quality?",
      a: "Built-in evaluation compares multiple answer modes and tracks metrics like faithfulness and accuracy — so you can prove quality before rolling out to your team.",
    },
    {
      q: "How do we get started?",
      a: "Request a demo and we'll walk you through chat, document upload, and quality reporting tailored to your organization's needs.",
    },
    {
      q: "How do we request a demo?",
      a: `Email us at ${CONTACT_EMAIL} or click any "Request a demo" button on this page.`,
    },
  ],
};

export const finalCta = {
  title: "Ready to see DomainMind in action?",
  description:
    "Schedule a demo and we'll walk you through chat, document upload, and quality reporting.",
  button: "Request a demo",
};

export const pillars = [
  { label: "Trustworthy", description: "Every answer points to source documents" },
  { label: "Proven", description: "Quality is measured, not assumed" },
  { label: "Secure", description: "Multi-tenant isolation and encryption" },
  { label: "Purpose-built", description: "Fine-tuned for compliance, not general chat" },
];
