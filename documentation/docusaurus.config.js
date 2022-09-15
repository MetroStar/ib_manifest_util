// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Iron Bank Manifest Utility',
  tagline: 'Making an update to your IB container just got easier',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/ib_manifest_util',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'MetroStar', // Usually your GitHub org/user name.
  projectName: 'ib_manifest_util', // Usually your repo name.
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: "/",
          path: "docs",
          sidebarPath: require.resolve('./sidebars.js'),
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Iron Bank Manifest Utility',
        logo: {
          alt: 'Iron Bank Logo',
          src: 'img/ib_logo.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'introduction',
            position: 'right',
            label: 'Docs',
            },
          {
            type: 'doc',
            docId: 'getting-started/installation',
            position: 'right',
            label: 'Getting Started',
          },
          {
            type: 'doc',
            docId: 'community/contributing',
            position: 'right',
            label: 'Community',
          },
          {
            href: 'https://github.com/MetroStar/ib_manifest_util',
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
                label: 'Getting Started',
                to: 'getting-started/installation',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Open an Issue',
                href: 'https://github.com/MetroStar/ib_manifest_util/issues',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/MetroStar/ib_manifest_util',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} MetroStar. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
