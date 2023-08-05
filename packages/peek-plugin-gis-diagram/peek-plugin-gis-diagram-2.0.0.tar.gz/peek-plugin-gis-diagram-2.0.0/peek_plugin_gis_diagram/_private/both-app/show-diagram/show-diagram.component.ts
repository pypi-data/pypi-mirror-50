import {Location} from "@angular/common";
import {Component} from "@angular/core";
import {ActivatedRoute, Params, Router} from "@angular/router";
import {Observable} from "rxjs/Observable";
import "rxjs/add/observable/zip";

import {
    DiagramCoordSetService,
    DiagramCoordSetTuple,
    DiagramPositionService,
    PositionUpdatedI
} from "@peek/peek_plugin_diagram";

import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";
import {modelSetKey} from "@peek/peek_plugin_gis_diagram/_private/PluginNames";
import {zip} from "rxjs/operators";

@Component({
    selector: 'plugin-gis-diagram-show-diagram',
    templateUrl: 'show-diagram.component.web.html',
    moduleId: module.id
})
export class ShowDiagramComponent extends ComponentLifecycleEventEmitter {


    constructor(private route: ActivatedRoute,
                private router: Router,
                private diagramCoordSetService: DiagramCoordSetService,
                private diagramPosService: DiagramPositionService,
                private loc: Location) {
        super();

        Observable.zip(
            this.diagramPosService.isReadyObservable().filter(v => v), // Only true
            diagramCoordSetService.diagramCoordSetTuples(modelSetKey)
                .filter(t => t.length != 0),
            (isReady: boolean, tuples: DiagramCoordSetTuple[]) => (tuples)
        )
            .takeUntil(this.onDestroyEvent)
            .subscribe((tuples: DiagramCoordSetTuple[]) => {
                    this.route.params
                        .takeUntil(this.onDestroyEvent)
                        .subscribe((params: Params) => this._applyRouteParams(params, tuples));
                }
            );

        this.diagramPosService
            .positionUpdatedObservable()
            .takeUntil(this.onDestroyEvent)
            .debounce(() => Observable.interval(1000))
            .subscribe((pos: PositionUpdatedI) => {
                let url = this.router.url.split(';')[0];

                // Sometimes it can try to position after we've navigated away
                if (url.indexOf('peek_plugin_gis_diagram') == -1)
                    return;

                this.router.navigate([url, {x: pos.x, y: pos.y, zoom: pos.zoom}]);
            });
    }


    private _applyRouteParams(params, tuples: DiagramCoordSetTuple[]): void {
        let vars = {};

        if (typeof window !== 'undefined') {
            window.location.href.replace(
                /[?&]+([^=&]+)=([^&]*)/gi,
                (m, key, value) => vars[key] = value
            );
        }

        let x = params['x'] || vars['x'];
        let y = params['y'] || vars['y'];
        let zoom = params['zoom'] || vars['zoom'] || '1.0';

        let dispKey = params['key'] || vars['key'];
        let coordSetKey = tuples[0].key;


        if (dispKey != null) {
            this.diagramPosService.positionByKey(
                modelSetKey, coordSetKey, {highlightKey:dispKey}
            );

        } else if (x != null && y != null) {
            this.diagramPosService.position(
                coordSetKey, parseFloat(x), parseFloat(y), parseFloat(zoom), {}
            );

        } else {
            this.diagramPosService.positionByCoordSet(coordSetKey);
        }
    }
}