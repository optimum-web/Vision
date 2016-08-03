import React from 'react';
import Panel from 'react-bootstrap/lib/Panel';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import Button from 'react-bootstrap/lib/Button';
import Radio from 'react-bootstrap/lib/Radio';
import ButtonToolbar from 'react-bootstrap/lib/ButtonToolbar';
import {findDOMNode} from 'react-dom';


const ChooseTestForm = React.createClass({



    render: function () {
        return (
            <div className="col-xs-4">
                <form className="" method="post" action="#" onSubmit={this._onSubmit} onChange={this._onChange}>
                        <Panel header="Choose Test Profile">
                            <div>
                                <Radio name="choice">
                                    Fluid Profile
                                </Radio>
                                <Radio name="choice">
                                    Electrical Profile
                                </Radio>

                                <ButtonToolbar>
                                    <Button bsStyle="success" type="submit">save</Button>
                                    <Button bsStyle="danger" >cancel</Button>
                                </ButtonToolbar>
                            </div>
                        </Panel>
                </form>
            </div>
        );
    }
});

export default ChooseTestForm;