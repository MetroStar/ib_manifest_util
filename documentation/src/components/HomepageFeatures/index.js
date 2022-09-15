import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';
import {
    BrowserRouter as Router,
    Link,
    Route,
    Switch,
  } from 'react-router-dom';


const FeatureList = [
  {
    title: <Link to="/getting-started/installation">Installation</Link>,
    Svg: require('@site/static/img/construction.svg').default,
    imageLink: "/docs/getting-started/installation",
    description: (
      <>
        Getting started using the IB Manifest Util is straightforward and takes
        less than 5 minutes to get set up.
      </>
    ),
  },
  {
    title: <Link to="/getting-started/installation">Update your IB Container</Link>,
    Svg: require('@site/static/img/update.svg').default,
    description: (
      <>
        Need to add a package? IB Manifest Util provides a single high-level command
        for generating all the files you'll need to update your container repo!
      </>
    ),
  },
  {
    title: <Link to="/community/contributing">Community</Link>,
    Svg: require('@site/static/img/contribute.svg').default,
    description: (
      <>
        We welcome contributions and questions from the community :)
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
