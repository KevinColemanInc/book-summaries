import React from "react";

import classes from "./Summary.module.css";
import { truncStr } from "./utils";

const Summary = props => {
  const { summary, chapter, vote_average } = props.item;

  return (
    <div
      className={classes.Container}
    >
        <p className={classes.VoteContainer}>Chapter {(chapter)}.</p>
        <p className={classes.Title}>{(summary)}</p>
    </div>
  );
};

export default Summary;
