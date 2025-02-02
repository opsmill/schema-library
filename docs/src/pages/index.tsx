import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Home(): React.JSX.Element {
 const {siteConfig} = useDocusaurusContext();
 return (
   <Layout
     title={`${siteConfig.title}`}
     description="Description will go into a meta tag in <head />"
   >
     <main>
       <div className="container margin-top--lg">
         <h1>Demo</h1>
       </div>
     </main>
   </Layout>
 );
}