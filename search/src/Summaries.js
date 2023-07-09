import React from "react";

import Summary from "./Summary";
import classes from "./Summaries.module.css";

const Summaries = ({ list, query }) => {
  let cards = <h3>Loading...</h3>;

  if (list) {
    cards = list.map((m, i) => <Summary key={i} item={m} query={query} />);
  }

  return (
    <div className={classes.Container}>
      <div className={classes.ContainerInner}>{cards}</div>
    </div>
  );
};

export default Summaries;
