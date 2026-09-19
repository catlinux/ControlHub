import js from "@eslint/js";
import vue from "eslint-plugin-vue";
import tsParser from "@typescript-eslint/parser";
import globals from "globals";

export default [
  {
    ignores: ["dist/**", "node_modules/**"],
  },
  js.configs.recommended,
  ...vue.configs["flat/essential"],
  {
    files: ["**/*.vue"],
    languageOptions: {
      globals: globals.browser,
      parserOptions: {
        parser: tsParser,
      },
    },
  },
];
