// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { SidePanelModel } from './SidePanelModel';
import { SidePanel } from './SidePanel';
import { EXTENSION_SPEC_VERSION } from './version';

const EXTENSION_ID = 'sidepanel';


function activate(app: JupyterFrontEnd, registry: IJupyterWidgetRegistry): void {
  let AppSidePanel = class extends SidePanel {
    constructor(options: any) {
      // console.log('activate sidepanel. options=', options);
      super({app, ...options});
    }
  };

  registry.registerWidget({
    name: EXTENSION_ID,
    version: EXTENSION_SPEC_VERSION,
    exports: {
      SidePanelModel: SidePanelModel,
      SidePanel: AppSidePanel
    }
  });
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activate,
  autoStart: true
};

export default  plugin;
