// Copyright 2018 Red Hat, Inc
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

import * as React from 'react'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import { parse } from 'query-string'

import { fetchLogfileIfNeeded } from '../actions/logfile'
import Refreshable from '../containers/Refreshable'
import LogFile from '../containers/logfile/LogFile'


class LogFilePage extends Refreshable {
  static propTypes = {
    match: PropTypes.object.isRequired,
    remoteData: PropTypes.object,
    tenant: PropTypes.object,
  }

  updateData = (force) => {
    this.props.dispatch(fetchLogfileIfNeeded(
      this.props.tenant,
      this.props.match.params.buildId,
      this.props.match.params.file,
      force))
  }

  componentDidMount () {
    document.title = 'Zuul Build Logfile'
    super.componentDidMount()
  }

  componentDidUpdate () {
    const line = this.props.location.hash.substring(1)
    if (line) {
      const element = document.getElementsByName(line)
      if (element.length) {
        element[0].scrollIntoView()
      }
    }
  }

  render () {
    const { remoteData } = this.props
    const build = this.props.build.builds[this.props.match.params.buildId]
    const severity = parse(this.props.location.search).severity
    return (
      <React.Fragment>
        <div style={{float: 'right'}}>
          {this.renderSpinner()}
        </div>
        {remoteData.data && <LogFile build={build} data={remoteData.data} severity={severity}/>}
      </React.Fragment>
    )
  }
}

export default connect(state => ({
  tenant: state.tenant,
  remoteData: state.logfile,
  build: state.build
}))(LogFilePage)
