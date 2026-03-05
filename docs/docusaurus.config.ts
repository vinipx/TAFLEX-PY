import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'TAFLEX PY',
  tagline: 'Enterprise Test Automation Framework in Python',
  favicon: 'img/logo.svg',

  url: process.env.DOCS_URL || 'https://vinipx.github.io',
  baseUrl: process.env.DOCS_BASE_URL || '/TAFLEX-PY/',

  organizationName: 'vinipx',
  projectName: 'taflex-py',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/vinipx/taflex-py/tree/main/docs/',
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    image: 'img/docusaurus-social-card.jpg',
    announcementBar: {
      id: "taflex_ts_v1",
      content:
        '⚡ TAFLEX PY — Unified Enterprise Test Automation for Web, API & Mobile. <a target="_blank" rel="noopener noreferrer" href="https://github.com/vinipx/taflex-py">Star us on GitHub</a>',
      backgroundColor: "#111111",
      textColor: "#d4d4d8",
      isCloseable: true,
    },
    mermaid: {
      theme: {
        light: "base",
        dark: "dark",
      },
    },
    navbar: {
      title: 'TAFLEX PY',
      logo: {
        alt: 'TAFLEX PY Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docs',
          position: 'left',
          label: 'Documentation',
        },
        {
          to: "/docs/getting-started/quickstart",
          label: "Getting Started",
          position: "left",
        },
        {
          to: "/docs/architecture/overview",
          label: "Architecture",
          position: "left",
        },
        {
          type: "dropdown",
          label: "Tutorials",
          position: "left",
          items: [
            { label: "Web Testing", to: "/docs/tutorials/web-tests" },
            { label: "BDD Testing", to: "/docs/tutorials/bdd-tests" },
            { label: "API Testing", to: "/docs/tutorials/api-tests" },
            { label: "Mobile Testing", to: "/docs/tutorials/mobile-tests" },
            { label: "Contract Testing", to: "/docs/tutorials/contract-testing" },
            { label: "Testing in the Cloud", to: "/docs/tutorials/cloud-execution" },
          ],
        },
        {
          type: "dropdown",
          label: "Core Guides",
          position: "left",
          items: [
            { label: "AI-Agent Integration (MCP)", to: "/docs/guides/mcp-integration" },
            { label: "Reporting Governance", to: "/docs/guides/reporting" },
            { label: "Pact Testing", to: "/docs/guides/pact-testing" },
            { label: "Locators", to: "/docs/guides/locators" },
            { label: "API Testing", to: "/docs/guides/api-testing" },
            { label: "BDD Testing", to: "/docs/guides/bdd-testing" },
            { label: "Cloud Testing", to: "/docs/guides/cloud-testing" },
            { label: "Database", to: "/docs/guides/database" },
            { label: "Unit Testing", to: "/docs/guides/unit-testing" },
          ],
        },
        {
          to: "/docs/api/core-interfaces",
          label: "API Reference",
          position: "left",
        },
        {
          type: "dropdown",
          label: "Guides",
          position: "left",
          items: [
            {
              to: "/docs/guides/qa-engineers",
              label: "QA Engineers",
            },
            {
              to: "/docs/guides/developers",
              label: "Developers",
            },
            {
              to: "/docs/guides/managers",
              label: "Managers",
            },
          ],
        },
        {
          type: "dropdown",
          label: "Resources",
          position: "left",
          items: [
            {
              to: "/docs/best-practices/test-design",
              label: "Best Practices",
            },
            {
              to: "/docs/troubleshooting/common-issues",
              label: "Troubleshooting",
            },
            {
              to: "/docs/contributing/guidelines",
              label: "Contributing",
            },
            {
              to: "/docs/changelog",
              label: "Changelog",
            },
          ],
        },
        {
          href: 'https://github.com/vinipx/taflex-py',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} TAFLEX PY. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'typescript'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
