import {
   output
} from '@jupyter-widgets/jupyterlab-manager';

import {
  EXTENSION_SPEC_VERSION
} from './version';

const MODULE_NAME = 'sidepanel';

export
class SidePanelModel extends output.OutputModel {
  rendered: boolean;

  defaults() {
    return {...super.defaults(),
      _model_name: SidePanelModel.model_name,
      _model_module: SidePanelModel.model_module,
      _model_module_version: SidePanelModel.model_module_version,

      _view_name: SidePanelModel.view_name,
      _view_module: SidePanelModel.view_module,
      _view_module_version: SidePanelModel.view_module_version,
      title: 'SidePanel',
      side: 'split-right',
      ref: null
    };
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.widget_manager.display_model(undefined, this, {});
  }

  static serializers : any = {
      ...output.OutputModel.serializers,
    };

  static model_name = 'SidePanelModel';
  static model_module = MODULE_NAME;
  static model_module_version = EXTENSION_SPEC_VERSION;

  static view_name = 'SidePanel2';
  static view_module = MODULE_NAME;
  static view_module_version = EXTENSION_SPEC_VERSION;
}
