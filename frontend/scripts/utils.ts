export function connect(){
    const sb = useSupabaseClient();
    return sb;
}

export async function getdata(table: string, query: string, where: string, what: string) {
    const l = await connect().from(table);

    let data = await l.select(query).eq(where, what).order("id", {ascending: false});
    // @ts-ignore
    return data["data"]![0][query];
}

export async function datafetch(table: string, query: string) {
    const l = await connect().from(table);
    let data = await l.select(query).order("id", {ascending:false});
    return data["data"]
}


export const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
