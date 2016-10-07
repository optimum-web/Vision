import {Component} from 'react';
import React from 'react';
// import EquipmentList from '../EquipmentList';
import TestResultForm from '../TestResultForm';
import EquipmentTestForm from '../EquipmentTestForm';
import TreeComponent from '../TreeComponent';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import FormControl from 'react-bootstrap/lib/FormControl';
import ControlLabel from 'react-bootstrap/lib/ControlLabel';

var Home = React.createClass({

    getInitialState: function () {
        return {
            source: '/api/v1.0/campaign/',
            text: ''
        }
    },

    onTreeSearch: function (e) {
        this.setState({
            searchValue: e.target.value
        });
        this.refs.tree.handleTreeSearch(e.target.value);
    },

    onTreeNodeClick: function (treeItem) {

        // console.log('got equipment id from tree click', typeof treeItem.equipment_id);
        // null comes as string in case no equipment assigned to tree item, condition from below should be removed later
        var id = (treeItem.equipment_id != 'null') ? treeItem.equipment_id : 0; 
        var src = '/api/v1.0/test_result/?equipment_id=' + id;

        this.setState({
            source: src
        });
        this.refs.testResultList.updateSource(this.state.source);
    },

    render: function () {
        console.log("SOURCE",this.state.source);
        console.log("HOME STATE", this.state);
        return (
            <div>
                <div className="col-md-3 equal_col">
                    <div className="maxwidth">
                        <FormGroup>
                            <ControlLabel>Search equipment</ControlLabel>
                            <FormControl
                                type="text"
                                placeholder="Search equipmemt"
                                ref="search"
                                id="plugins4_q"
                                className="input col-md-12"
                                onKeyUp={this.onTreeSearch}/>
                        </FormGroup>
                        <br/>
                        <br/>
                        <br/>
                        <br/>
                        <TreeComponent
                            ref="tree"
                            struct={treeStruct}
                            onTreeNodeClick={this.onTreeNodeClick}
                        />
                    </div>
                </div>
                <div className="col-md-9">
                    <TestResultForm ref="testResultList"
                                    source={this.state.source}
                                    />
                </div>
            </div>
        )
    }
});
export default Home;
