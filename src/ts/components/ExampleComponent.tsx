import React from 'react';
import {DashComponentProps} from '../props';

type Props = {
    // Insert props
} & DashComponentProps;

/**
 * Component description
 */
const ExampleComponent = (props: Props) => {
    const { id } = props;
    return (
        <div id={id}>
            <h1>Hello Word</h1>
        </div>
    )
}

ExampleComponent.defaultProps = {};

export default ExampleComponent;
