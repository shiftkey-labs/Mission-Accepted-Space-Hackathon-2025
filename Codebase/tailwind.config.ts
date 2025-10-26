import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "rgb(5, 10, 25)",
        foreground: "rgb(240, 250, 255)",
        card: "rgb(10, 15, 35)",
        "card-foreground": "rgb(240, 250, 255)",
        popover: "rgb(10, 15, 35)",
        "popover-foreground": "rgb(240, 250, 255)",
        primary: "rgb(59, 130, 246)",
        "primary-foreground": "rgb(255, 255, 255)",
        secondary: "rgb(139, 92, 246)",
        "secondary-foreground": "rgb(255, 255, 255)",
        muted: "rgb(30, 35, 55)",
        "muted-foreground": "rgb(156, 163, 175)",
        accent: "rgb(16, 185, 129)",
        "accent-foreground": "rgb(255, 255, 255)",
        destructive: "rgb(239, 68, 68)",
        "destructive-foreground": "rgb(255, 255, 255)",
        border: "rgb(30, 41, 59)",
        input: "rgb(30, 41, 59)",
        ring: "rgb(59, 130, 246)",
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
