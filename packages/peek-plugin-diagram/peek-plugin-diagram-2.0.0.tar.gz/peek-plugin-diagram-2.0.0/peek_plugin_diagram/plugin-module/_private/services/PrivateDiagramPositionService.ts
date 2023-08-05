import {Injectable} from "@angular/core";
import {
    DiagramPositionService,
    DispKeyLocation,
    OptionalPositionArgsI,
    PositionUpdatedI
} from "../../DiagramPositionService";
import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";

import {DispKeyLocationTuple} from "../location-loader/DispKeyLocationTuple";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {PrivateDiagramLocationLoaderService} from "../location-loader";


export interface DiagramPositionI {
    coordSetKey: string;
    x: number;
    y: number;
    zoom: number;
    opts: OptionalPositionArgsI;
}


export interface DiagramPositionByKeyI {
    modelSetKey: string;
    coordSetKey: string | null;
    opts: OptionalPositionArgsI;
}


export interface DiagramPositionByCoordSetI {
    coordSetKey: string | null;
}


@Injectable()
export class PrivateDiagramPositionService extends DiagramPositionService {

    constructor(private locationIndexService: PrivateDiagramLocationLoaderService,
                private balloonMsg: Ng2BalloonMsgService) {
        super();

    }

    // This observable is for when the canvas updates the title
    private titleUpdatedSubject: Subject<string> = new Subject<string>();

    private positionByCoordSetSubject = new Subject<string>();
    private positionSubject = new Subject<DiagramPositionI>();
    private positionByKeySubject = new Subject<DiagramPositionByKeyI>();

    private isReadySubject = new Subject<boolean>();

    private postionUpdatedSubject = new Subject<PositionUpdatedI>();

    positionByCoordSet(coordSetKey: string): void {
        this.positionByCoordSetSubject.next(coordSetKey);
    }

    position(coordSetKey: string, x: number, y: number, zoom: number,
             opts: OptionalPositionArgsI = {}): void {
        this.positionSubject.next({
            coordSetKey: coordSetKey,
            x: x,
            y: y,
            zoom: zoom,
            opts
        });
    }

    async positionByKey(modelSetKey: string,
                        coordSetKey: string | null,
                        opts: OptionalPositionArgsI = {}): Promise<void> {

        if (opts.highlightKey == null || opts.highlightKey.length == 0)
            throw new Error("positionByKey must be passed opts.highlightKey");

        const dispKeyIndexes: DispKeyLocationTuple[] = await this.locationIndexService
            .getLocations(modelSetKey, opts.highlightKey);

        if (dispKeyIndexes.length == 0) {
            this.balloonMsg.showError(
                `Can not locate disply item ${opts.highlightKey}`
                + ` in model set ${modelSetKey}`
            );
        }

        for (let dispKeyIndex of dispKeyIndexes) {
            // If we've been given a coord set key
            // and it doesn't match the found item:
            if (coordSetKey != null && dispKeyIndex.coordSetKey != coordSetKey) {
                continue;
            }

            this.positionSubject.next({
                coordSetKey: dispKeyIndex.coordSetKey,
                x: dispKeyIndex.x,
                y: dispKeyIndex.y,
                zoom: 2.0,
                opts
            });
            return;
        }

        this.balloonMsg.showError(
            `Can not locate disply item ${opts.highlightKey}`
            + ` in model set ${modelSetKey}, in coord set ${coordSetKey}`
        );

    }

    async canPositionByKey(modelSetKey: string, dispKey: string): Promise<boolean> {
        const val: DispKeyLocationTuple[] = await this.locationIndexService
            .getLocations(modelSetKey, dispKey);
        return val.length != 0;
    }

    async locationsForKey(modelSetKey: string, dispKey: string): Promise<DispKeyLocation[]> {
        const tuples: DispKeyLocationTuple[] = await this.locationIndexService
            .getLocations(modelSetKey, dispKey);

        const locations = [];
        const locationByCoordSet = {};
        for (const tuple of tuples) {
            let location = locationByCoordSet[tuple.coordSetKey];
            if (location == null) {
                location = {
                    modelSetKey: modelSetKey,
                    coordSetKey: tuple.coordSetKey,
                    dispKey: dispKey,
                    positions: [],
                    zoom: 2.0
                };
                locationByCoordSet[tuple.coordSetKey] = location;
                locations.push(location);
            }
            location.positions.push({x: tuple.x, y: tuple.y});
        }
        return locations;
    }

    setReady(value: boolean) {
        this.isReadySubject.next(true);
    }

    setTitle(value: string) {
        this.titleUpdatedSubject.next(value);
    }

    positionUpdated(pos: PositionUpdatedI): void {
        this.postionUpdatedSubject.next(pos);
    }

    isReadyObservable(): Observable<boolean> {
        return this.isReadySubject;
    }

    positionUpdatedObservable(): Observable<PositionUpdatedI> {
        return this.postionUpdatedSubject;
    }


    titleUpdatedObservable(): Observable<string> {
        return this.titleUpdatedSubject;
    }

    positionObservable(): Observable<DiagramPositionI> {
        return this.positionSubject;
    }

    positionByKeyObservable(): Observable<DiagramPositionByKeyI> {
        return this.positionByKeySubject;
    }

    positionByCoordSetObservable(): Observable<string> {
        return this.positionByCoordSetSubject;
    }

}