import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  schemaSidebar: [
    'home',
    {
      type: 'category',
      label: 'Reference',
      collapsed: false,
      items: [
        'reference/extensions',
      ],
    },
    'contributing',
  ]
};

export default sidebars;
