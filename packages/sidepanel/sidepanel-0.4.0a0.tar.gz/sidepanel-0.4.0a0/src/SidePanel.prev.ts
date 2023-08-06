import { find } from '@phosphor/algorithm';
import { UUID } from '@phosphor/coreutils';
import { Message, MessageLoop } from '@phosphor/messaging';

import { JupyterLab } from '@jupyterlab/application';
import { IOutputAreaModel } from '@jupyterlab/outputarea';

import {output} from  "@jupyter-widgets/jupyterlab-manager";

import { SidePanelModel } from './SidePanelModel';
import '../css/SidePanel.css';


export
class SidePanel extends output.OutputView {


  constructor(options: any) {
    super(options);
    this.app = options.app;
  }

  refresh(model:IOutputAreaModel, args:IOutputAreaModel.ChangedArgs)  {
    MessageLoop.postMessage(this._outputView, new Message('resize'));
  }

  render() {
    console.log('sidepanel: render()');
    super.render();
    if (!this.model.rendered) {
      let w = this._outputView;
      w.addClass('sidepanel');
      w.addClass('jp-LinkedOutputView');
      w.title.label = this.model.get('title');
      w.title.closable = true;
      w.id = UUID.uuid4();
      w.model.changed.connect(this.refresh, this);
      if (Object.keys(this.model.views).length > 1) {
        w.node.style.display = 'none';
        let key = Object.keys(this.model.views)[0];
        this.model.views[key].then((v: SidePanel) => v._outputView.activate());
      } else {
        let shell = this.app.shell;
        let label = this.model.get('ref');
        let ref_id:any = null;
        if (label) {
          let ref = find(shell.widgets('main'), w => w.title.label == label);
          if (ref) ref_id = ref.id;
        }
        shell.add(w, 'main', {mode : this.model.get('side'), ref:ref_id});
        // shell.activateById(w.id);
      }
    }
  }

  app: JupyterLab;
  model: SidePanelModel;
}


// export
// class SidePanel extends OutputView {
//
//
//   constructor(options: any) {
//     super(options);
//     this.app = options.app;
//   }
//
//   _createElement(tagName: string) {
//     this.pWidget = new output.JupyterPhosphorPanelWidget({ view: this });
//     return this.pWidget.node;
//   }
//
//   _setElement(el: HTMLElement) {
//     if (this.el || el !== this.pWidget.node) {
//       // Boxes don't allow setting the element beyond the initial creation.
//       throw new Error('Cannot reset the DOM element.');
//     }
//
//     this.el = this.pWidget.node;
//     this.$el = $(this.pWidget.node);
//   }
//
//   refresh(model:IOutputAreaModel, args:IOutputAreaModel.ChangedArgs)  {
//     MessageLoop.postMessage(this._outputView, new Message('resize'));
//   }
//
//   render() {
//     console.log('sidepanel: renden()');
//     if (!this.model.rendered) {
//       super.render();
//       this._outputView = new SimplifiedOutputArea({
//         rendermime: this.model.widget_manager.rendermime,
//         contentFactory: SimplifiedOutputArea.defaultContentFactory,
//         model: this.model.outputs
//       });
//
//       this.pWidget.insertWidget(0, this._outputView);
//
//       this.pWidget.addClass('jupyter-widgets');
//       this.pWidget.addClass('widget-output');
//       this.update();
//
//       let w = this._outputView;
//       w.addClass('sidepanel');
//       w.addClass('jp-LinkedOutputView');
//       w.title.label = this.model.get('title');
//       w.title.closable = true;
//       w.id = UUID.uuid4();
//       w.model.changed.connect(this.refresh, this);
//       if (Object.keys(this.model.views).length > 1) {
//         w.node.style.display = 'none';
//         let key = Object.keys(this.model.views)[0];
//         this.model.views[key].then((v: SidePanel) => v._outputView.activate());
//       } else {
//         let shell = this.app.shell;
//         let label = this.model.get('ref');
//         let ref_id:any = null;
//         if (label) {
//           let ref = find(shell.widgets('main'), w => w.title.label == label);
//           if (ref) ref_id = ref.id;
//         }
//         shell.add(w, 'main', {mode : this.model.get('side'), ref:ref_id});
//         // shell.activateById(w.id);
//       }
//     }
//   }
//
//   remove() {
//     console.log('sidepanel: remove()')
//     this._outputView.dispose();
//     return super.remove();
//   }
//
//   app: JupyterLab;
//   model: SidePanelModel;
//   _outputView: SimplifiedOutputArea;
//   pWidget: Panel
// }