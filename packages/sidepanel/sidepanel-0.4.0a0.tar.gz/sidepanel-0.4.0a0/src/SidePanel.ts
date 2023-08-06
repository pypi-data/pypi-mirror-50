import * as $ from 'jquery';

import { JupyterLab } from "@jupyterlab/application";
import { MainAreaWidget } from '@jupyterlab/apputils';
import { IOutputAreaModel, SimplifiedOutputArea } from '@jupyterlab/outputarea';

import { DOMWidgetView } from '@jupyter-widgets/base';
import { OutputView } from "@jupyter-widgets/output";

import { find } from '@phosphor/algorithm';
import { Message, MessageLoop } from '@phosphor/messaging';
import { UUID } from '@phosphor/coreutils';
import { Panel } from '@phosphor/widgets';

import {SidePanelModel} from "./SidePanelModel";
import '../css/SidePanel.css';

export
class SidePanel extends OutputView {
  constructor(options: any) {
    // console.log('SidePanel2', options);
    super(options);
    this.app = options.app;
  }

  _createElement(tagName: string):any {
    // console.log('create element', tagName);
    this.pWidget = new SidePanelOutputArea({ view: this });
    return this.pWidget.node;
  }

  _setElement(el: HTMLElement) {
    // console.log('set element', el);
    if (this.el || el !== this.pWidget.node) {
        throw new Error('Cannot reset the DOM element.');
    }
    this.el = this.pWidget.node;
    this.$el = $(this.pWidget.node);
  }

 render() {
    super.render();
    this.outputArea = new SimplifiedOutputArea({
      rendermime: this.model.widget_manager.rendermime,
      contentFactory: SimplifiedOutputArea.defaultContentFactory,
      model: this.model.outputs
    });
    this.outputArea.addClass('sidepanel');
    this.outputArea.addClass('jp-LinkedOutputView');
    this.update();

    let shell = this.app.shell;
    let w = new MainAreaWidget({content: this.outputArea});
    w.id = `SidePanel-${UUID.uuid4()}`;
    w.title.label = this.model.get('title') || '';
    w.title.closable = true;

    this.outputArea.model.changed.connect(this.refresh, this);

    let ref_id:any = null;
    let label = this.model.get('ref');
    if (label) {
      let ref = find(shell.widgets('main'), w => w.title.label == label);
      if (ref) ref_id = ref.id;
    }
    shell.add(w, 'main', {mode : this.model.get('side'), ref:ref_id});
 }

  refresh(model:IOutputAreaModel, args:IOutputAreaModel.ChangedArgs)  {
    // console.log('sidepanel.referesh', model, args);
    MessageLoop.postMessage(this.outputArea, new Message('resize'));
  }

 remove() {
    this.outputArea.dispose();
    return super.remove();
 }

  app: JupyterLab;
  model: SidePanelModel;
  pWidget: Panel;
  outputArea: SimplifiedOutputArea;
}

//
// SidePanelOutputArea
//
class SidePanelOutputArea extends Panel {
  constructor(options:any) {
    let view = options.view;
    delete options.view;
    super(options);
    this._view = view;
  }

  processMessage(msg: Message) {
      super.processMessage(msg);
      this._view.processPhosphorMessage(msg);
  }

  dispose() {
    if (this.isDisposed) {
        return;
    }
    super.dispose();
    if (this._view) {
        this._view.remove();
    }
    this._view = null;
  }

    private _view: DOMWidgetView;
}