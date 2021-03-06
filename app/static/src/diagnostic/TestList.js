import React from 'react';
import FormGroup from 'react-bootstrap/lib/FormGroup';
import FormControl from 'react-bootstrap/lib/FormControl';
import Accordion from 'react-bootstrap/lib/Accordion';
import Panel from 'react-bootstrap/lib/Panel';
import {Link} from 'react-router';
import NewTestForm from './NewTestForm';
import Button from 'react-bootstrap/lib/Button';
import Table from 'react-bootstrap/lib/Table';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import ReactDOM from 'react-dom';

var TestItem = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })
    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: true
        };
    },

    componentDidMount: function () {
    },

    componentWillUnmount: function () {
    },

    onRemove: function () {
        var data = this.props.data;
        // Deleted id id in edited at the moment
        if (this.props.editedId == data.id) {
            NotificationManager.info('Cannot remove because this test is edited at the moment.');
            return false;
        }

        var url = '/api/v1.0/test_result/' + data.id;
        var that = this;
        $.authorizedAjax({
            url: url,
            type: 'DELETE',
            dataType: 'json',
            contentType: 'application/json',
            beforeSend: function () {},
            success: function () {
                that.props.reloadList();
                NotificationManager.success('Test has been deleted successfully');
            },
            error: function () {
                NotificationManager.error('Sorry an error occurred');
            },
            complete: function () {}
        });

    },

    onDuplicate: function () {
        var data = this.props.data;
        var testResultId = data.id;
        var url = '/api/v1.0/test_result/' + testResultId + '/duplicate';
        var that = this;
        $.authorizedAjax({
            url: url,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            beforeSend: function () {
            },
            success: function (data) {
                that.props.reloadList();
                if (data.result === null) {
                    NotificationManager.info('This test cannot be copied as it is private and doesn\'t belong to you');
                } else {
                    NotificationManager.success('Test has been duplicated successfully');
                }
            },
            error: function () {
                NotificationManager.error('Sorry an error occurred');
            },
            complete: function () {
            }
        });
    },

    edit: function () {
        this.props.editTestForm(this.props.data.id);
    },

    render: function () {

        if (!this.state.isVisible) {
            return (<div></div>);
        }
        var test = this.props.data;
        var test_status = test.test_status;
        var test_type_name = 'Undetermined - click to configure';
        if  (test.test_type_id) {
            test_type_name = (test.test_type_id == 10) ? 'Fluid':'Electrical';
        }
        var performed_by_name = (test.performed_by != null) ? test.performed_by.name : 'undetermined';

        return (
            <tr>
                <td>
                    <a href="javascript: void(0);" onClick={this.edit}>{test_type_name}</a>
                </td>
                <td>{test.analysis_number}</td>
                <td>{test_status.name}</td>
                <td>{performed_by_name}</td>
                <td>
                    <a href="javascript:void(0)"
                       className="glyphicon glyphicon-remove text-danger"
                       onClick={this.onRemove}
                       aria-hidden="true">
                    </a>
                </td>
                <td>
                    <a href="javascript:void(0)"
                       onClick={this.onDuplicate}
                       className="glyphicon glyphicon-duplicate text-success"
                       aria-hidden="true">
                    </a>
                </td>
            </tr>
        );
    }
});

var TestItemList = React.createClass({

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })
    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: true,
            showTestForm: false,
            showAddTestButton: true,
            editedId: null
        };
    },

    componentDidMount: function () {
        // load test_result and show tests for each equipment
        // this.serverRequest = $.authorizedGet(this.props.source, function (result) {
        //     items = (result['result']);
        //     this.setState({
        //         items: items
        //     });
        // }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        // this.serverRequest.abort();
    },

    showTestForm: function () {
        var data = {
            campaign_id: this.props.campaign_id,
            equipment_id: this.props.id
        };

        this.serverRequest = $.authorizedAjax({
            url: '/api/v1.0/test_result/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function () { this.setState({loading: true}) }.bind(this),
            success: function (result) {
                         var id = result['result'];
                         this.editTestForm(id)
                     }.bind(this)
        });
    },

    closeTestForm: function () {
        this.setState({
            showTestForm: false
        })
    },

    editTestForm: function (id) {
        if (typeof id == 'undefined') {
            return null;
        }

        this.refs.new_test_form._edit(id);
        this.setState({
            showTestForm: true,
            editedId: id
        })
    },

    reloadList: function () {
        this.closeTestForm();
        this.props.reloadList();
    },

    render: function () {
        var equipment_id = this.props.id;
        var tests = [];
        var data = {
            campaign_id: this.props.campaign_id,
            equipment_id: this.props.id
        };
        var showTestForm = this.state.showTestForm;
        var showAddTestButton = this.state.showAddTestButton;
        for (var i = 0; i < this.props.data.length; i++) {
            var item = this.props.data[i];
            if (item.equipment.id == equipment_id) {

                if (item.performed_by_id === null && item.test_reason_id === null) {
                    data = item;
                    showTestForm = true;
                    showAddTestButton = false;

                    NotificationManager.warning('Please choose reason of testing and performer.', null, 6000);
                    continue;
                }

                tests.push(<TestItem key={item.id}
                                     data={item}
                                     editTestForm={this.editTestForm}
                                     reloadList={this.props.reloadList}
                                     editedId={this.state.editedId}/>)
            }
        }

        //for (var key in this.props.data) {
        //    if (this.props.data[key] instanceof Object && Object.keys(this.props.data[key]).length){
        //        tests.push(
        //            <TestItem data={this.props.data[key]}
        //                      key={this.props.data[key].id}/>
        //        );
        //    }
        //}

        return (
            <div>
                <div className="row">
                    <div className="col-md-12">
                        <Table responsive hover id="test_prof">
                            <thead>
                            <tr>
                                <th className="col-md-2">Test name</th>
                                <th className="col-md-1">Analisys number</th>
                                <th className="col-md-1">Status</th>
                                <th className="col-md-2">Performed by</th>
                                <th className="col-md-1">Delete</th>
                                <th className="col-md-1">Duplicate</th>
                            </tr>
                            </thead>
                            <tbody>
                            {tests}
                            </tbody>
                        </Table>
                    </div>
                </div>

                {showAddTestButton ?
                <div className="row">
                    <div className="col-md-3">
                        <FormGroup>
                            <Button onClick={this.showTestForm} className="success">Add more tests</Button>
                        </FormGroup>
                    </div>
                </div>
                    :null}

                <NewTestForm ref="new_test_form"
                             show={showTestForm}
                             handleClose={this.closeTestForm}
                             reloadList={this.reloadList}
                             data={data}
                />
            </div>
        );
    }
});


var TestList = React.createClass({

    contextTypes: {
        router: React.PropTypes.object
    },

    handleChange: function (event, index, value) {
        this.setState({
            value: event.target.value
        })
    },

    getInitialState: function () {
        return {
            items: [],
            isVisible: true
        };
    },

    componentDidMount: function () {

        var campaign_id = this.props.params.campaign;
        var url = '/api/v1.0/test_result/?campaign_id=' + campaign_id;
        this.serverRequest = $.authorizedGet(url,
            function (result) {

                var tests = result['result'];
                var equipment = [];

                tests.map(function (item) {
                    equipment[item.equipment.id] = item.equipment;
                });

                this.setState({
                    campaign_id: campaign_id,
                    equipment: equipment,
                    tests: tests
                });

            }.bind(this), 'json');
    },

    componentWillUnmount: function () {
        this.serverRequest.abort();
    },

    reloadList: function () {
        this.componentDidMount();
    },

    startCampaign: function (e) {
        e.preventDefault();
        NotificationManager.success('Campaign has been successfully started');
        this.finishSetup();
        this.context.router.push(this.refs.startCampaign.props.to);
    },

    finishSetup: function () {
        var url = '/api/v1.0/campaign/' + this.props.params.campaign + '/finish';
        $.authorizedGet(url);
    },

    render: function () {

        var items = [];
        var equipment_id;
        for (var key in this.state.equipment) {
            equipment_id = this.state.equipment[key].id;
            items.push(
                <Panel
                    key={this.state.equipment[key].id}
                    
                    header={this.state.equipment[key].name}
                >
                    <TestItemList data={this.state.tests}
                                  id={this.state.equipment[key].id}
                                  campaign_id={this.state.campaign_id}
                                  reloadList={this.reloadList}
                    />
                </Panel>
            );
        }
        return (
            this.state.isVisible ?
                <div>
                    <div className="row">
                        <Accordion>
                            {items}
                        </Accordion>
                            <div className="row">
                                <div className="col-md-offset-10 col-md-2">
                                    <FormGroup className="pull-right">
                                        <Link to={"/" + equipment_id}
                                              className="btn btn-success"
                                              onClick={this.startCampaign}
                                              ref="startCampaign">Finish Setup</Link>
                                    </FormGroup>
                                </div>
                            </div>
                    </div>
                </div> : null
        );
    }
});

export default TestList;
