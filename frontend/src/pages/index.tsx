import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Learning →
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Comprehensive textbook on Physical AI and Humanoid Robotics for technical developers">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h3>🤖 Comprehensive Coverage</h3>
                <p>
                  12 modules covering ROS 2, simulation, NVIDIA Isaac, VLA systems,
                  locomotion, manipulation, perception, and deployment.
                </p>
              </div>
              <div className="col col--4">
                <h3>💡 AI-Powered Q&A</h3>
                <p>
                  Interactive chatbot answers questions using RAG technology -
                  all responses grounded in textbook content, no hallucinations.
                </p>
              </div>
              <div className="col col--4">
                <h3>🎯 Practical Focus</h3>
                <p>
                  Every chapter includes Concepts, Architectures, Algorithms,
                  and Real-World Considerations for production deployment.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
