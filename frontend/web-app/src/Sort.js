import React from "react";

const compare = (a, b) => {
    return formatDate(b.date)-formatDate(a.date);
}

const formatDate = (stringDate) => {
    const splitted = stringDate.split("/");
    return new Date(splitted[2]+'-'+splitted[1]+'-'+splitted[0]);

}

const Sort = ({children, by}) => {
    if(!by) {
        return children;
    } else {
        console.log("test1");
        return React.Children.toArray(children).sort(compare)
    }
}

export default Sort;