import React from "react";

import classes from "./Summary.module.css";
import { truncStr } from "./utils";

const Summary = props => {
  const { summary, poster_path, vote_average } = props.item;

  return (
    <div
      className={classes.Container}
    >
        <p className={classes.Title}>{(summary)}</p>
    </div>
  );
};

export default Summary;
