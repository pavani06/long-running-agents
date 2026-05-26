// eslint.config.js — Shared ESLint configuration
//
// Plugins:
//   - @eslint/js recommended — standard JS quality rules
//   - eslint-plugin-n          — Node.js best practices (auto-detects ESM from package.json)
//   - eslint-plugin-unicorn    — cherry-picked rules

import js from "@eslint/js";
import n from "eslint-plugin-n";
import unicorn from "eslint-plugin-unicorn";
import globals from "globals";
import noCatchMessage from "./eslint-rules/no-catch-message.js";
import noRawConsoleInScripts from "./eslint-rules/no-raw-console-in-scripts.js";

export default [
  // ── Global ignores ──────────────────────────────────────────────────
  {
    ignores: [
      "node_modules/**",
      "artifacts/**",
      ".runtime/**",
      ".opencode/**",
      ".planning/**",
      ".worktrees/**",
      "coverage/**",
      "docs/**",
    ],
  },

  // ── ESLint core recommended ────────────────────────────────────────
  js.configs.recommended,

  // ── Node.js plugin (reads "type":"module" from package.json) ───────
  n.configs["flat/recommended"],

  // ── Project-wide overrides ─────────────────────────────────────────
  {
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.node,
      },
    },
    plugins: {
      unicorn,
      local: { rules: { "no-catch-message": noCatchMessage, "no-raw-console-in-scripts": noRawConsoleInScripts } },
    },
    rules: {
      // Unicorn — cherry-picked only
      "unicorn/no-thenable": "error",

      // Core — errors (must never happen)
      "no-var": "error",
      "no-unused-vars": ["error", {
        argsIgnorePattern: "^_",
        caughtErrorsIgnorePattern: "^_",
        destructuredArrayIgnorePattern: "^_",
      }],
      "prefer-const": "error",
      "eqeqeq": ["error", "always", { null: "ignore" }],
      "no-useless-assignment": "error",
      "no-await-in-loop": "error",
      "preserve-caught-error": "error",

      // Catch-block safety — custom rule
      "local/no-catch-message": "error",

      // Node.js plugin tuning
      "n/no-missing-import": "error",
      "n/no-unpublished-import": "error",
      "n/no-unsupported-features/node-builtins": ["error", {
        ignores: ["fetch", "test", "test.describe", "test.it", "test.mock", "test.mock.module"],
      }],
    },
  },

  // ── Script file overrides ───────────────────────────────────────────
  {
    files: ["scripts/**/*.js"],
    rules: {
      "n/no-process-exit": "off",
      "n/hashbang": "off",
      "no-empty": "warn",
      "n/no-missing-import": "off",
      "local/no-raw-console-in-scripts": "warn",
    },
  },

  // ── Test file overrides ────────────────────────────────────────────
  {
    files: ["tests/**/*.js"],
    rules: {
      "n/no-process-exit": "off",
      "no-empty": "warn",
      "n/no-missing-import": "off",
    },
  },
];
